install:
	mkdir -p ~/.local/share/pop-launcher/plugins/floww
	cp -r ./plugin/* ~/.local/share/pop-launcher/plugins/floww
	chmod +x ~/.local/share/pop-launcher/plugins/floww/floww.py

uninstall:
	rm -rf ~/.local/share/pop-launcher/plugins/floww


