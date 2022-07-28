all: clean client

clear:
	clear

dependencies:
	pip install -r requirements.txt

clean:
	@echo "Cleanning..."
	-rm -f $(BINARY_NAME)
	-rm -f $(BINARY_UNIX)
	-rm -f $(BINARY_SPEC)
	-rm -rf build
	-rm -rf dist
	@echo "Done cleanning."

client:
	@echo "Building client..."
	pyinstaller --onefile ./src/client.py
	mv ./dist/$(BINARY_NAME) ./
	@echo "Done client."

run:
	./$(BINARY_NAME)



BINARY_NAME=client
BINARY_UNIX=$(BINARY_NAME)_unix
BINARY_SPEC=$(BINARY_NAME).spec