RANGE_DIRECTORY=$1
DESTINATION="/global/scratch/groups/dh/aanderson/ocr_pages"

#Define module function and MODULEPATH since ipynb doesn't have them in its execution environment
export MODULEPATH=/global/home/groups/consultsw/sl-7.x86_64/modfiles:/global/home/groups/consultsw/sl-6.x86_64/modfiles:/global/software/sl-6.x86_64/modfiles/tools:/global/software/sl-6.x86_64/modfiles/langs:/clusterfs/vector/home/groups/software/sl-6.x86_64/modfiles:/global/home/groups/vector/software/sl-6.x86_64/modfiles/langs

module ()
{
    eval `/usr/Modules/bin/modulecmd bash $*`
}

if [[ $1 == "" ]]; then
    echo "Usage: ./FindSumerianZipOCR.sh /path/to/folder/with/hocr"
    exit 1
fi

cd $RANGE_DIRECTORY

PDFS=$(ls *.pdf)
echo $PDFS

module load zip

for PDF in $PDFS; do
    PDF=$(echo $PDF | cut -d . -f 1)
    mkdir $PDF
    cp ${PDF}-*.hocr $PDF/.
    zip -r ${PDF}.zip $PDF
done

chmod 775 *.zip
mv *.zip $DESTINATION
