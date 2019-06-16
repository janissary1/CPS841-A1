You can run the programs through command line with python 2.7+
e.g
python q1.py
python q2.py

This way does not show matplotlib graphs

You can also edit values for each algorithm from the command line before running
Make sure you either choose to run the program with all necessary command line arguments or none of them like above.
e.g:
#python q1.py $rounds $constant_value
python q1.py 5000 0.05 
e.g
#python q2.py $rounds $alpha1 $beta1 $alpha2 $beta2
python q2.py 10000 0.1 0.1 0.1 0.0 //doesn't work nvm
OR JUST
python q2.py //just uses basic values above

Additionally, you may execute the compiled executable, compiled using PyInstaller,
it should be cross compatible for Linux/Windows/MacOS, (thats what the site said).
This will include Matplotlib graphs if you want a nicer view of whats happening instead of raw output.

