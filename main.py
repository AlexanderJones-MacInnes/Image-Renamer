import os, json, sys, subprocess

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

#Set up client object with an API key
#Either input from a .env or by the user at launch
def CreateClient():
    #Try to find API key in .env
    load_dotenv(find_dotenv())

    try:
        client = OpenAI(api_key = os.getenv("OPEN_API_KEY"))

    #If key is not found prompt the user for one
    except:
        while True:
            print("API key invalid or not found.\nPlease input one now.")
            key = input("Enter API key: ")
            try:
                client = OpenAI(api_key = key)
                #Throw a generic prompt at the AI to validate if the key works
                resp = client.responses.create(
                    model = "gpt-4o",
                    input = [{"role" : "user", "content" : "test"}]
                )
                break
            except:
                pass

        while True:
            print("Do you want to save this for next time? (Y/N)")
            usrChoice = input()
            if usrChoice == "Y" or usrChoice == "y":
                env = open(".env","wt")
                env.write(f"OPEN_API_KEY = {key}")
                env.close()
                break
            if usrChoice == "N" or usrChoice == "n":
                break
    return client

model = "gpt-4o"

#Prompt the AI to check file extensions. Seems more versatile than having a whitelist of extensions.
#Errors out sometimes but that's handled if it does.
tools = [
    {
        "type" : "function",
        "name" : "InspectImageFile",
        "description" : "Discern if the input file is an image",
        "parameters" : {
            "type" : "object",
            "properties" : {
                "IsImage" : {
                    "type" : "boolean"
                },
                "Extension" : {
                    "type" : "string",
                    "description" : "The file extension of the image."
                }
            }
        }
    }
]

def lRemove(s:str,charList:list[str]):
    """Removes a list of characters from the input string."""
    for char in charList:
        s = s.replace(char,"")
    return s

def CreateFile(path:str):
    """
    Takes an input file path and returns a file id for AI prompting

    :argument path: A string representing the file path to create a file-id for
    """
    with open(path, "rb") as f:
        result = client.files.create(
            file=f,
            purpose="vision"
        )
    return result.id

#The main meat of this program. Prompts the AI with images and renames them.
def RenameImage(path):
    print(f"Checking if {path} is an image...")
    checkImg = client.responses.create(
        model = model,
        input = [{
            "role": "user",
            "content": f"Is {path} an image?"
        }],
        tools = tools
    )
    checkImgResults = json.loads(checkImg.output[0].arguments)

    if checkImgResults["IsImage"] == True:
        try:
            print(f"Prompting AI with {path}")
            result = client.responses.create(
                model = model,
                input = [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": "Produce a short, yet descriptive name for this image."
                            },
                            {
                                "type": "input_image",
                                "file_id": CreateFile(path.lower())
                            }
                        ]
                    }
                ]
            )
            try:
                newName = lRemove(result.output_text,[":", "-", "_", "\""])
                newName += "." + checkImgResults["Extension"].lower()
                print("Generated name: " + newName)

                os.rename(path, os.path.dirname(path) + "/" + newName)
            except:
                print("Unable to rename file")

        except Exception as e:
            print(f"Failed to inspect file. Perhaps {path} is not an image?")
            print(f"Error: {e}")
            pass

    else:
        print(f"{path} is not an image.")

#Path for recursive file searching program
searchPath = os.path.dirname(__file__) + "/RecursiveSearch.exe"

#Handle input args for launching from command-line
argv = sys.argv

if argv[1] == "help":
    print("This is a command line tool for automatically renaming folders of images")
    print("Proper syntax for usage is as follows:")
    print("ImageRenamer <File Path|Folder Path>")
    print(r"EG: ImageRenamer 'C:\Pictures\MyPhotos'")

else:
    client = CreateClient()
    inputPath = argv[1]

    if os.path.isdir(inputPath):
        searchDir = subprocess.run(
        [
            searchPath,
            inputPath,
            "/a"
        ],
            text = True,
            capture_output = True
        )
        fileList = searchDir.stdout.strip().split("\n")
        for file in fileList:
            RenameImage(file)
    else:
        RenameImage(inputPath)
