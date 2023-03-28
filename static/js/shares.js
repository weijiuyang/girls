// import ApexCharts from "apexcharts"

var options = {
  chart: {
    type: 'bar'
  },
  series: [{
    name: 'sales',
    data: [30,40,45,50,49,60,70,91,125]
  }],
  xaxis: {
    categories: [1991,1992,1993,1994,1995,1996,1997, 1998,1999]
  }
}


t = document.getElementById("fff")
console.log(t.text)
console.log(t.txt)
console.log(t.content)
console.log(t)




var chart = new ApexCharts(document.getElementById("chart"), options);

chart.render();