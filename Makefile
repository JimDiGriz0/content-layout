install:
	@npm init -y \
	&& npm pkg set type=module \
	&& npm pkg set "scripts.test=jest --colors" \
	&& mkdir -p __tests__ \
	&& touch index.html \
	&& echo 'node_modules/' > .gitignore \
	&& echo '.npmrc' >> .gitignore


first-git:
	@git add . \
	&& git commit -m 'first commit'

test:
	@npx jest

test2:
	@npm test -s
