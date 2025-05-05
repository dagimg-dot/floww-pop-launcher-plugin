install:
	mkdir -p ~/.local/share/pop-launcher/plugins/floww
	cp -r ./plugin/* ~/.local/share/pop-launcher/plugins/floww
	chmod +x ~/.local/share/pop-launcher/plugins/floww/floww.py

uninstall:
	rm -rf ~/.local/share/pop-launcher/plugins/floww

release:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION is not set. Usage: make release VERSION=x.y.z"; \
		exit 1; \
	fi
	@echo "Creating and pushing tag v$(VERSION)..."
	git tag v$(VERSION)
	git push origin v$(VERSION)


