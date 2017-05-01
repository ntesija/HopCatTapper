// $(document).ready(function() {
//     var path = window.location.pathname;
//     var splitPath = path.split('/');
//     var location = splitPath[2];
//     console.log(location);
//     $.get("/api/v1/beers/" + location, function(data)  {
//         console.log(data);
//         $('#beer-list').append(data.data);
//     });
// });