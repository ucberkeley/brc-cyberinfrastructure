RANGE_DIRECTORY=$1
DESTINATION="/global/scratch/groups/dh/aanderson/ocr_pages"

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
