build:
	cd src && ./ecc template.bpf.c template.h

run:
	cd src && sudo ./ecli run package.json

clean:
	cd src && rm *.json *.o
