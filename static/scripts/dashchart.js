$(function() {
  var ctx = document.getElementById('myChart').getContext('2d');
  var chart = new Chart(ctx, {
      // The type of chart we want to create
      type: 'bar',

      // The data for our dataset
      data: {
          labels: ["January", "February", "March", "April", "May", "June", "July"],
          datasets: [{
              label: "Revenue",
              backgroundColor: '#EF9F00',
              borderColor: '#232323',
              data: [0, 0, 0, 0, 0, 0, 0],
          }]
      },

      // Configuration options go here
      options: {}
  });
});
