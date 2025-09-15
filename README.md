# Image-Renamer
An Open AI API program that automatically renames folders of images.

**Being a program that uses the Open AI API you will require an API key to make use of this program.**
You can enter your API key through a .env included in the root directory of Image-Renamer. The program will also prompt you to input one if no key was found.

This program is a Windows command-line utilty so it lacks a GUI. <br>
You can display some help text by entering: `Image-Renamer help` <br>

Typical convention for usage is to enter: `Image-Renamer <path>` <br>
<path> can be an image file or folder of image files. The program will also process any folders contained within the initial folder that was set to `<path>` <br>

This program is dependant on an external exe *(RecursiveSearch.exe)* for it's file searching capabilities. 
I was mostly doing this as a test and this will probably be changed in later versions. 
RecursiveSearch.exe is bundled with the main release-exe through the use of Pyinstaller.
So this detail shouldn't matter to or impede a typical end-user.
