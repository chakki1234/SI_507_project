$('#search').click(function(){
    m_name = $('#textbox').val()
    console.log(m_name)
    window.location.href = `/${m_name}`;
})


$.ajax({
    url: `/movie_specific/${$('#mname').text()}`,
    type: 'GET',
    success: function(data) {
        if (data != 'No'){
            let {Title, year_lang_plot_node, Genre, Director_Actor, Rating, Poster, Reviews, Similar_movies, Recommended_movies, Flatrate, Buy, Rent, youtube} = data
        
            $('#error').hide()
            $('#content').show()

            // poster
            $('#poster').attr('src', Poster);
            
            // Genre and Director 
            $('#genre').append(`
            <button href="#" class="badge rounded-pill text-bg-warning mt-2" style="font-family: 'Roboto Condensed', sans-serif;">${Genre}</button>
            `)
            $('#genre').append(`
            <button href="#" class="badge rounded-pill text-bg-warning mt-2" style="font-family: 'Roboto Condensed', sans-serif;">Director : ${Director_Actor[0]}</button>
            `)
    
            // youtube
            $('#trailer').attr('src', `https://www.youtube.com/embed/${youtube}?autoplay=1&mute=1`)
    
            // Rating
            $('#rating').text(`IMDb Rating : ${Rating}`)
    
            // Title
            $('#mname').text(`${Title.toUpperCase()} - ${year_lang_plot_node[1]} (${year_lang_plot_node[0]})`)
            $('#mname').css('color', '#E5E5CB')
    
            // Plot
            $('#plot').text(year_lang_plot_node[2])
    
            // Cast
            let cast_array = Director_Actor[1].split(',');
            cast_array.forEach(function(element){
                $('#cast').append(`
                    <div class="d-flex flex-row justify-content-center">
                        <h5>${element}</h5>
                    </div>
                `)
            });
    
            // reviews
            if (Reviews.length == 0){
                $('#reviews').append(`
                <div class="d-flex flex-row mb-3">
                <p style="color: #E5E5CB;">No reviews available</p>
                </div>
                `)
            }
            else{
            Reviews.forEach(function(element){
                $('#reviews').append(`
                <div class="d-flex flex-column col-3">
                <div class="d-flex flex-row justify-content-center" style="border-bottom: 1px solid #E5E5CB;">
                  <h5 style="color: #E5E5CB;" >Review by ${element[0]}</h5>
                </div>
                <div class="p-2">
                  <p class='text_packup' style='color: #E5E5CB;' >${element[1]}</p>
                </div>
                </div>
                `)
            })
            }
    
    
            // Similar 
            if (Similar_movies.length == 0){
                $('#similar').append(`
                <div class="d-flex flex-row m-3">
                <p style="color: #E5E5CB;">No Similar movies available</p>
                </div>
                `)
            }
            else {
            Similar_movies.forEach(element => {
                let newElem = $(`
                <div class="card col-2 ml-1 mr-2" style='border: none; background-color: #111111;'>
                <img src="https://image.tmdb.org/t/p/w500/${element[1]}" class="card-img-top" alt="..."> 
                <div class="card-body d-flex flex-column justify-content-between">
                    <a href='/${element[0]}' style="text-decoration: none;"><h5 class='m-1' style="font-size: 15px; color: #03C988; font-family: 'Roboto Condensed', sans-serif">${element[0]}</h5></a>
                    <button href="#" class="col-12 badge rounded-pill text-bg-warning mt-2" style="font-family: 'Roboto Condensed', sans-serif;">Rating : ${element[2]}</button>
                </div>
                </div>`
                );
                $('#similar').append(newElem)
            });
            }
    
            // Recommended movies
            if (Recommended_movies.length == 0){
                $('#recommended').append(`
                <div class="d-flex flex-row m-3">
                <p style="color: #E5E5CB;">No Recommendations available</p>
                </div>
                `)
            }
            else {
            Recommended_movies.forEach(element => {
                let newElem = $(`
                <div class="card col-2 ml-1 mr-2" style='border: none; background-color: #111111;'>
                <img src="https://image.tmdb.org/t/p/w500/${element[1]}" class="card-img-top" alt="..."> 
                <div class="card-body d-flex flex-column justify-content-between">
                    <a href='/${element[0]}' style="text-decoration: none;"><h5 class='m-1' style="font-size: 15px; color: #03C988; font-family: 'Roboto Condensed', sans-serif">${element[0]}</h5></a>
                    <button href="#" class="col-12 badge rounded-pill text-bg-warning mt-2" style="font-family: 'Roboto Condensed', sans-serif;">Rating : ${element[2]}</button>
                </div>
                </div>`
                );
                $('#recommended').append(newElem)
            });
            }
        
            // Watch providers
            Flatrate.forEach(function(ele){
                $('#flatrate').append(`
                <a href="#" class="list-group-item" style="background-color: #111111; color: #E5E5CB;">${ele}</a>
                `)
            })
    
            Buy.forEach(function(ele){
                $('#buy').append(`
                <a href="#" class="list-group-item" style="background-color: #111111; color: #E5E5CB;">${ele}</a>
                `)
            })
    
            Rent.forEach(function(ele){
                $('#rent').append(`
                <a href="#" class="list-group-item" style="background-color: #111111; color: #E5E5CB;">${ele}</a>
                `)
            })
        }
       else{
        // $('#content').hide()
        $('#error').show()
        $('#content').hide()
        $('#error_txt').text(`Could not match the search results. Check your spelling.`)
        $('#error_txt').css('color', '#E5E5CB')

       }

    },
    error: function(xhr, status, error) {
        console.log('failed')
    }
  });
