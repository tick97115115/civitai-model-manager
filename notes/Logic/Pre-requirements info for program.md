# Intro part

## What are the needs of for program startup?

The project consists of:
1. model file download. (from CivitAI)
	- for Chinese user they need use proxy.
2. local model management.
	- the location of lora folder
3. database store and retrieve metadata info.
	- the location of database

So we figured out what configuration info the user need to provide before running program.

and there is one more thing that need to be decide, which is where we store the config file and what format should it be?

summary:
1. where we store the config file and what format should it be?
2. store these config info
	1. proxy (optional)
	2. lora_folder (neccessary)
	3. db_uri

## where we store the config file and what format should it be?

For simplicity, I will create a config.py script to manage configuration reading and writing, and it will create a .config file next to itself if ".config" doesn't exists.





