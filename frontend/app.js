
function textSearch() {
    var searchText = document.getElementById('search_query');
    if (!searchText.value) {
        alert('Please enter a valid text or voice input!');
    } else {
        searchText = searchText.value.trim().toLowerCase();
        console.log('Searching Photos....');
        searchPhotos(searchText);
    }
    
}

function searchPhotos(searchText) {
    console.log(searchText);
    document.getElementById('search_query').value = searchText;
    document.getElementById('photos_search_results').innerHTML = "<h4 style=\"text-align:center\">";

    var params = {
        'q': searchText
    };

    var additionalParams = {
        headers: {
            'x-api-key': '6CMczQa7eN7h4a70uBTAP157xzqmBj8B3pVBGZ22'
        }
    };
    var apigClient = apigClientFactory.newClient({
        apiKey: '6CMczQa7eN7h4a70uBTAP157xzqmBj8B3pVBGZ22'
    });

    apigClient.searchGet(params, {}, additionalParams)
        .then(function(result) {
            console.log("Search results:", result);
            var photos = result.data.results;
            var photosDiv = document.getElementById("photos_search_results");
            photosDiv.innerHTML = "";  
            photos.forEach(function(photo) {
                photosDiv.innerHTML += '<figure><img src="' + photo + '" style="width:100px"></figure>';
            });
        }).catch(function(result) {
            var photosDiv = document.getElementById("photos_search_results");
            photosDiv.innerHTML = "No Photos Found!";
            console.log(result);
        });
}

function uploadPhoto() {
 
    var file = document.getElementById('uploaded_file').files[0];
    if (!file) {
        alert("Please select a file to upload.");
        return;
    }
   
   
    var customLabelsInput = document.getElementById('custom_labels').value;
   
    var customLabels = customLabelsInput.split(',')
                                         .map(label => label.trim())
                                         .filter(label => label.length > 0) // Filters out empty strings
                                         .join(','); // This will be an empty string if no valid labels are provided

    console.log(customLabels)

    var headers = {
        'Content-Type': "image/" + file.name.split('.').pop(),
        'x-amz-meta-customLabels': customLabels,
        'x-api-key': '6CMczQa7eN7h4a70uBTAP157xzqmBj8B3pVBGZ22'
    };


    var reader = new FileReader();
    reader.readAsArrayBuffer(file);

/*
    reader.onload = function () {
        const arrayBuffer = reader.result;
       
        const apigClient = apigClientFactory.newClient();
        const additionalParams = {
            headers: headers
        };
        console.log(arrayBuffer)
        
        apigClient.uploadObjectPut({object: photoFile.name, 'x-amz-meta-customlabels': customLabels}, arrayBuffer, additionalParams)
            .then(function (response) {
                console.log("Upload successful:", result);
                alert('Upload successful!');
            }).catch(function (error) {
                console.error('Upload failed:', error);
                alert('Upload failed. See console for details.');
            });
    };
    */
    const additionalParams = {
        headers: headers
    };

    url = "https://photos-bucket-3.s3.amazonaws.com/" + file.name
    axios.put(url, file, additionalParams).then(response => {
       alert("Image uploaded: " + file.name);
    });

}


