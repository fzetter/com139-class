// Config
const datast = stacked_json
const marginst = {top: 30, bottom: 75, right: 40, left: 75}
const widthst = $("#stacked-chart").width() - margin.left - margin.right
const heightst = $("#stacked-chart").height() - margin.top - margin.bottom
const gst = d3.select("#stacked-chart").append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")")

// Scales
const x_stacked_scale = d3.scaleBand().range([0, widthst]).padding(0.2)
const y_stacked_scale = d3.scaleLinear().rangeRound([0, heightst])
const color_scale_stacked = d3.scaleOrdinal(d3.schemeSpectral[11])

// Parse & Formatters
const parseDate = d3.timeParse('%Y')
const formatSi = d3.format(".3s")
const formatNumber = d3.format(".1f")
const formatBillion = x => formatNumber(x / 1e9)

// Axis Generators
const yAxis_stacked = d3.axisLeft(y_stacked_scale).tickFormat(formatBillion)
const xAxis_stacked = d3.axisBottom(x_stacked_scale)
const y_axis_stacked = gst.append("g").attr("class", "y axis")
const x_axis_stacked = gst.append("g").attr("class", "x axis").attr("transform", "translate(0," + height + ")")

// Y-Axis label
const y_label_stacked = y_axis_stacked.append("text")
	  .attr("class", "axis-title")
    .attr("y", 6)
    .attr("transform", "rotate(-90)")
    .attr("dy", "0.71em")
    .attr("text-anchor", "end")

// area_stacked Chart & Stack
const area_stacked = d3.area()
	.x(d => x_stacked_scale(d.data.date))
	.y0(d => y_stacked_scale(d[0]))
	.y1(d => y_stacked_scale(d[1]))

const stack = d3.stack()
let columns = [], states = []

// Legend
const legend_stacked = gst.append("g").attr("transform", "translate(" + (width + 170) + "," + (height - 210) + ")")

// Config
datast.filter(key => {
  states.push(key["STATE"])
  const keys = Object.keys(key).filter(curr => curr !== 'STATE')
  columns = keys
})

x_stacked_scale.domain(columns)
y_stacked_scale.domain([2152, 0])
color_scale_stacked.domain(columns)

// // Stack Chart
// stack.keys(columns)
// 	.order(d3.stackOrderNone)
// 	.offset(d3.stackOffsetNone)
//
// const browser = gst.selectAll('.browser')
// 	.data(stack(datast))
// 	.enter().append('g')
// 	.attr('class', d => 'browser ' + d.key)
// 	.attr('fill-opacity', 0.5)
//
// browser.append('path')
// 	.attr('class', 'area_stacked')
// 	.attr('d', area_stacked)
// 	.style('fill', d => color_scale_stacked(d.key))
//
// Axis & Labels
configAxisAndLabelsSt(x_stacked_scale, y_stacked_scale, "Billions of liters", "#fff")



// Config Axis
// ***********
function configAxisAndLabelsSt(x, y, yLabel, color) {

  // Y Axis
  y_axis_stacked.call(yAxis_stacked).selectAll("text").style("fill", color)

  // X Axis
  x_axis_stacked.call(xAxis_stacked).selectAll("text").style("fill", color)
    .attr("y", "10").attr("x", "-5")
    .attr("text-anchor", "end")
    .attr("transform", "rotate(-45)")

  // // Axis Color
  // gst.selectAll(".y.axis line").style("stroke", color)
  // gst.selectAll(".y.axis path").style("stroke", color)
  // gst.selectAll(".x.axis line").style("stroke", color)
  // gst.selectAll(".x.axis path").style("stroke", color)
  //
  // // Label
  // y_label_stacked.text(yLabel).style("fill", color)
  //
  // // Legend
  // columns.reverse().forEach((country, i) => {
  // 	const legendRow = legend_stacked.append("g").attr("transform", "translate(-15, " + ((i * 20)-30) + ")")
  // 	legendRow.append("rect")
  // 		.attr("width", 10)
  // 		.attr("height", 10)
  // 		.attr("fill", color_scale_stacked(country))
  // 	legendRow.append("text")
  // 	  .attr("class", "legend")
  // 		.attr("x", -10)
  // 		.attr("y", 10)
  // 		.attr("text-anchor", "end")
  // 		.style("text-transform", "capitalize")
  // 		.text(country)
  // })
  //
  // gst.selectAll(".legend").style("fill", color)

}

// NOTES:
// https://github.com/d3/d3-scale-chromatic
