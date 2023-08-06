"""Console script for container_patcher."""
import sys
import click
import docker
import os
import shutil
import tarfile
import re
import container_patcher.api as githubapi
import asyncio
import json


@click.command()
@click.argument('container')
@click.argument('pkg')
@click.argument('cve')
@click.option('--src', help='deb source URL')
@click.option('--key', help='gpg key file absolute path')
@click.option('--commit', help='Commit with modified target CVE')
def main(container, pkg, cve, src, key, commit):
    client = docker.from_env()
    tmp_host_path = '/tmp/.container-patcher'
    tmp_container_path = '/mnt/vol1'
    if not os.path.isdir(tmp_host_path):
        os.makedirs(tmp_host_path)
    else:
        shutil.rmtree(tmp_host_path)
        os.makedirs(tmp_host_path)

    dev_env = client.containers.run(
        'samasamahd/container-patcher',
        detach=True,
        tty=True,
        volumes={tmp_host_path: {'bind': tmp_container_path, 'mode': 'rw'}}
    )
    target_container = client.containers.get(container)

    # gitリポジトリの取得
    if not os.path.isdir(tmp_host_path + '/git-src'):
        os.makedirs(tmp_host_path + '/git-src')
    loop = asyncio.get_event_loop()
    pkg_repo = loop.run_until_complete(githubapi.get_search_repo(pkg))
    if pkg_repo is not None:
        if not click.confirm(f'Does the target repository match with {pkg_repo["full_name"]}?', 'y'):
            raise click.Abort()
        click.echo('Cloning Git Repository...')
        dev_env.exec_run(f'git clone {pkg_repo["html_url"]}', workdir=tmp_container_path + '/git-src')

    patched_commit = ''
    if commit is None:
        searched_commits = []
        click.echo('Searching commits...')
        # CVEの修正コミットを検索
        loop = asyncio.get_event_loop()
        res_commits = loop.run_until_complete(githubapi.get_search_commits(pkg_repo['full_name'], cve))
        searched_commits.extend(res_commits)

        # Issueからのコミット取得
        res_issues = loop.run_until_complete(githubapi.get_search_issues(pkg_repo['full_name'], cve))
        if not res_issues:
            for issue in res_issues:
                if issue["pull_request"] is not None:
                    pull_num = issue.split('/')[-1]
                    pull_commits = loop.run_until_complete(githubapi.get_pull_commits(pkg_repo['full_name'], pull_num))
                    searched_commits.extend(pull_commits)

        if searched_commits is None:
            click.echo(f'Commits not found about {cve}')
            raise click.Abort()
        else:
            set_of_jsons = {json.dumps(d, sort_keys=True) for d in searched_commits}
            suggest_commits = [json.loads(t) for t in set_of_jsons]
            click.echo(str(len(suggest_commits))+'items found.')
            for commit in suggest_commits:
                if click.confirm((f'Apply this patch?\n{commit["sha"]}\n{commit["commit"]["message"]}\n')):
                    patched_commit = commit["sha"]
                    break
            if not patched_commit:
                input_commit_sha = click.prompt('Input patched commit sha')
                if input_commit_sha != "":
                    patched_commit = input_commit_sha
                else:
                    click.echo('bye')
                    raise click.Abort()

    else:
        patched_commit = commit
    res = target_container.exec_run(
        ['/bin/bash',
         '-c',
         f'dpkg -l {pkg} | sed -ne \'6p\' | tr \' \' \'\\n\' | sed -e \'/^$/d\' | sed -ne \'3p\'']
    )
    old_ver = res[1].decode().replace('\n', '')

    # srcとkeyが指定されていた場合の処理
    if src is not None:
        dev_env.exec_run(['/bin/bash', '-c', f'echo \"deb {src}\" >> /etc/apt/sources.list'])
        dev_env.exec_run(['/bin/bash', '-c', f'echo \"deb-src {src}\" >> /etc/apt/sources.list'])
        if key is not None:
            if not os.path.isfile(key):
                print(f'{key} is not exist')
                raise click.Abort()
            key_name = os.path.basename(key)
            shutil.copyfile(key, tmp_host_path+'/'+key_name)

            dev_env.exec_run(f'apt-key add {tmp_container_path}/{key_name}')
        dev_env.exec_run('apt-get update')

    # ソースコードの取得処理
    click.echo('getting source code...')
    if not os.path.isdir(tmp_host_path+'/old-src'):
        os.makedirs(tmp_host_path+'/old-src')
    dev_env.exec_run(['/bin/bash', '-c', f'apt-get update'])
    get_src_res = dev_env.exec_run(
        ['/bin/bash', '-c', f'apt-get source {pkg}={old_ver}']
        , workdir=tmp_container_path+'/old-src'
    )

    # gitリポジトリの操作(パッチファイル作成)
    os.makedirs(tmp_host_path+'/.patch')
    git_src_path = tmp_container_path+'/git-src/'+pkg
    if os.path.isdir(tmp_host_path+'/git-src/'+pkg):
        dev_env.exec_run(
            ['/bin/bash', '-c', f'git checkout {patched_commit}'],
            workdir=git_src_path
        )

    # パッチを当てる処理
    click.echo('patching...')
    files = os.listdir(f'{tmp_host_path}/old-src')
    src_dirs = [f for f in files if os.path.isdir(os.path.join(f'{tmp_host_path}/old-src', f))]
    if len(src_dirs) != 0:
        dev_env.exec_run(
            ['/bin/bash', '-c', f'git diff HEAD HEAD~1 > {tmp_container_path}/.patch/diff.patch'],
            workdir=git_src_path
        )
        dev_env.exec_run(
            ['/bin/bash', '-c', f'patch -p1 -R < ../../.patch/diff.patch'],
            workdir=git_src_path
        )
    else:
        print(get_src_res[1].decode())

        click.echo('Package source codes is not found.')
        raise click.Abort()

    # ビルド周りの処理
    click.echo('building package...')
    dev_env.exec_run(
        ['/bin/bash', '-c', f'apt-get build-dep {pkg} -y']
    )

    dev_env.exec_run(
        ['/bin/bash', '-c', f'debuild -uc -us -b'],
        workdir=f'{tmp_container_path}/old-src/{src_dirs[0]}'
    )

    dev_env.exec_run(
        ['/bin/bash',
         '-c',
         'ls -1 | sed -ne \'/.deb$/p\' | sed -e \'/dbg/d\' | { read p ; dpkg -x \"$p\" /mnt/vol1/bin; }'
         ],
        workdir=tmp_container_path+'/old-src'
    )

    # ファイルを対象コンテナに転送
    container_bin = f'/usr/sbin/{pkg}'
    container_bin_debug = f'/usr/sbin/{pkg}-debug'
    host_bin = tmp_host_path+'/bin'+container_bin
    host_bin_debug = tmp_host_path+'/bin'+container_bin_debug

    if os.path.isfile(host_bin):
        copy_file_host_to_container(host_bin, container_bin, target_container)
    if os.path.isfile(host_bin_debug):
        copy_file_host_to_container(host_bin_debug, container_bin_debug, target_container)

    shutil.rmtree(tmp_host_path)
    dev_env.stop()
    dev_env.remove()

    click.echo('Patch completed!')
    return 0


def copy_file_host_to_container(src, dist, container):
    os.chdir(os.path.dirname(src))
    file_name = os.path.basename(src)
    tar = tarfile.open(src + '.tar', mode='w')
    try:
        tar.add(file_name)
    finally:
        tar.close()
    data = open(src + '.tar', 'rb').read()
    container.put_archive(os.path.dirname(dist), data)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
