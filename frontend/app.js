function searchPhotos() {
    const query = document.getElementById('searchQuery').value;
    const resultDiv = document.getElementById('searchResults');

    // Clear previous results
    resultDiv.innerHTML = '';

    // Assuming 'apigClient' is from the AWS API Gateway-generated SDK
    var apigClient = apigClientFactory.newClient({
        apiKey: '6CMczQa7eN7h4a70uBTAP157xzqmBj8B3pVBGZ22'
    });
    const params = {
        q: query // This is how you pass query parameters
    };

    print(query)

    apigClient.searchGet(params, {}, {})
        .then(function (response) {
            // Success handling
            const photos = response.data.results;
            console.log(photos)
            photos.forEach(photo => {
                const imgElement = document.createElement('img');
                imgElement.src = photo;
                imgElement.style.width = '100px';
                resultDiv.appendChild(imgElement);
                console.log(resultDiv)
            });
        }).catch(function (error) {
            // Error handling
            console.error('Search failed:', error);
            resultDiv.innerHTML = 'Search failed. See console for details.';
        });
}

function uploadPhoto() {
    const photoFile = document.getElementById('photoUpload').files[0];
    const customLabels = document.getElementById('customLabels').value;
    console.log("heeh")
    console.log(customLabels)
    const headers = {
        'Content-Type': "image/jpg",
        'x-amz-meta-customLabels': customLabels,
        'x-api-key': '6CMczQa7eN7h4a70uBTAP157xzqmBj8B3pVBGZ22'
    };
    console.log("heeh 1")
    //const blob = new Blob([photoFile])
    const reader = new FileReader();

    reader.readAsArrayBuffer(photoFile);
    console.log("heeh 2")
    reader.onload = function () {
        const arrayBuffer = reader.result;
        //const blob = new Blob([arrayBuffer], { type: 'image/jpg'});
        const apigClient = apigClientFactory.newClient();
        const additionalParams = {
            headers: headers
        };
        console.log("heeh 3")
        console.log(arrayBuffer)
        // Example assumes your API client expects an object key to be part of the path
        apigClient.uploadObjectPut({object: photoFile.name, 'x-amz-meta-customLabels': customLabels}, arrayBuffer, additionalParams)
            .then(function (response) {
                console.log("heeh 4")
                alert('Upload successful!');
            }).catch(function (error) {
                console.error('Upload failed:', error);
                alert('Upload failed. See console for details.');
            });
    };
}