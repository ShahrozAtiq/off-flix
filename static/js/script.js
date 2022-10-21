function part_nav() {
    select = document.querySelector('select')
    select.onchange = () => {
        url = document.URL
        url = url.split('/')
        url[url.length - 1] = select.value
        url = url.join('/')
        if (url !== document.URL)
            location.replace(url)
    }
}


function play(id){
    el = document.querySelector(`div[id="${id}"] span`)
    el.classList.add("episode-thumbnail-gradient")

    $.getJSON(`/play/${id}`,
        function (data) {
            //do nothing
        });
    }

function play_random(id){

    $.getJSON(`/random/${id}`,
        function (data) {
            //do nothing
        });
    }

window.onload = part_nav