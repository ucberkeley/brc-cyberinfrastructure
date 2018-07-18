import PhotoScan 
import time 
doc = PhotoScan.app.document 
chunk = PhotoScan.app.document.addChunk()
chunk.addPhotos( ["/opt/images/coffeecup-1.jpg","/opt/images/coffeecup-2.jpg","/opt/images/coffeecup-3.jpg","/opt/images/coffeecup-4.jpg"] )
doc.save(path="/opt/photoscan-test.psz", chunks = [doc.chunk])
