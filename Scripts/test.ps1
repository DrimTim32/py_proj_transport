$version = $args[0]
$files = ".eggs","py_proj_lights.egg-info",".cache"
$dir = ".\"
$pythonScript = "setup.py"
if( -Not (Test-Path "$dir$pythonScript")){
   cd ..
}
write-host "Starting tests..."
if($version -eq 2)
{
	write-host "Testing python 2"
	python2 .\setup.py -q test -q
}
elseif($version -eq 3)
{
	write-host "Testing python 3"
	python .\setup.py -q test -q
} 
else
{
	write-host "Testing python 2"
	python2 .\setup.py -q test -q
	write-host "Testing python 3"
	python .\setup.py -q test -q
}

write-host "Removing not important directories ..."
foreach($file in $files){
    if(Test-Path "$dir$file"){
        Remove-Item -Force -Recurse "$dir$file"
    }
}
write-host "Clearing compiled python files ..."
get-childitem ./ -include *.pyc -recurse | foreach ($_) {remove-item $_.fullname -recurse} 
get-childitem ./ -include *.egg -recurse | foreach ($_) {remove-item $_.fullname -recurse}  
get-childitem ./ -include __pycache__ -recurse | foreach ($_) {remove-item $_.fullname -recurse}
write-host "All done."