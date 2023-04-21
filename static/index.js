$('#search').click(function(){
    let m_name = $('#textbox').val()
    console.log(m_name)
    window.location.href = `/${m_name}`;
})

$('#textbox').on('keypress', function(e) {
    if (e.which === 13) {
        let m_name = $('#textbox').val()
        console.log(m_name)
        window.location.href = `/${m_name}`;
    }
  });

// Top Rated
$.ajax({
    url: '/top_rated_api_request',
    type: 'GET',
    success: function(data) {
        data.forEach(element => {

            let newElem = $(`
            <div class="card col-2 ml-1 mr-2" style='border: none; background-color: #111111;'>
            <img src="https://image.tmdb.org/t/p/w500/${element[1]}" class="card-img-top" alt="..."> 
            <div class="card-body d-flex flex-column justify-content-between">
                <a href='/${element[0]}' style="text-decoration: none;"><h5 class='m-1' style="font-size: 15px; color: #03C988; font-family: 'Roboto Condensed', sans-serif">${element[0]}</h5></a>
                <button href="#" class="col-12 badge rounded-pill text-bg-warning mt-2" style="font-family: 'Roboto Condensed', sans-serif;">Rating : ${element[2]}</button>
            </div>
            </div>`
            );
            $('#rated').append(newElem)
            
        });
    },
    error: function(xhr, status, error) {
        console.log('failed')
    }
  });

// Popular movies
  $.ajax({
    url: '/top_popular_api_request',
    type: 'GET',
    success: function(data) {
        data.forEach(element => {

            let newElem = $(`
            <div class="card col-2 ml-1 mr-2" style='border: none; background-color: #111111;'>
            <img src="https://image.tmdb.org/t/p/w500/${element[1]}" class="card-img-top" alt="..."> 
            <div class="card-body d-flex flex-column justify-content-between">
                <a href='/${element[0]}' style="text-decoration: none;"><h5 class='m-1' style="font-size: 15px; color: #03C988; font-family: 'Roboto Condensed', sans-serif">${element[0]}</h5></a>
                <button href="#" class="col-12 badge rounded-pill text-bg-warning mt-2" style="font-family: 'Roboto Condensed', sans-serif;">Rating : ${element[2]}</button>
            </div>
            </div>`
            );
            $('#popular').append(newElem)
            
        });
    },
    error: function(xhr, status, error) {
        console.log('failed')
    }
  });
  
// Trending movies today
$.ajax({
    url: '/top_trending_api_request',
    type: 'GET',
    success: function(data) {
     
        data.forEach(element => {
           
            let newElem = $(`
            <div class="card col-2 ml-1 mr-2" style='border: none; background-color: #111111;'>
            <img src="https://image.tmdb.org/t/p/w500/${element[1]}" class="card-img-top" alt="..."> 
            <div class="card-body d-flex flex-column justify-content-between">
                <a href='/${element[0]}' style="text-decoration: none;"><h5 class='m-1' style="font-size: 15px; color: #03C988; font-family: 'Roboto Condensed', sans-serif">${element[0]}</h5></a>
                <button href="#" class="col-12 badge rounded-pill text-bg-warning mt-2" style="font-family: 'Roboto Condensed', sans-serif;">Rating : ${element[2]}</button>
            </div>
            </div>`
            );
            $('#trending').append(newElem)
            
        });
    },
    error: function(xhr, status, error) {
        console.log('failed')
    }
  });

  
 
