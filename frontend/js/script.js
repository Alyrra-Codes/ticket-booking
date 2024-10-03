
const API_SERVER = 'http://localhost:5000'

var selectFlag = false

function getAttractions() {
    fetch(API_SERVER + '/attractions')
    .then(response => response.json())
    .then(data => {
        console.log(data)
        data.forEach(attraction => {
            console.log(attraction)
            createAttractionCard(attraction)
        })
    })
}
function goToPage(id){
    console.log('Navigate ' + id);
    window.location = 'select-time.html';
}

function handleSelectTime(id){
    e = document.getElementById(id)
    if(selectFlag == false){
        e.classList.add('selected')
        e.id = 'selected'
        selectFlag = true
    }
    else{
        if(id == 'selected'){   
            // remove class from previous selected time     
            s = document.getElementById('selected')
            s.classList.remove('selected')
            s.id = s.innerHTML
            selectFlag = false
        }
        else{
            // remove class from previous selected time
            s = document.getElementById('selected')
            s.classList.remove('selected')
            s.id = s.innerHTML
            // add class to new selection
            e.classList.add('selected')
            e.id = 'selected'
        }
    }

}

function submitTime() {
    time = document.getElementById('selected').innerHTML
    if(time == "09:00"){
        console.log(time) 
    }
}