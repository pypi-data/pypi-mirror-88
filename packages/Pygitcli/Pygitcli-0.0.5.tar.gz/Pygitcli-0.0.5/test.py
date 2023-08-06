import pygitcli
git = pygitcli.Git()
git.init()
git.add()
git.commit('Changed URL , branch fetching logic')
git.push()
