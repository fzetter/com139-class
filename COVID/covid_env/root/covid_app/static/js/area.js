// Config
const dataa = area_json
const margina = {top: 30, bottom: 75, right: 40, left: 75}
const widtha = $("#area-chart").width() - margin.left - margin.right
const heighta = $("#area-chart").height() - margin.top - margin.bottom
const ga = d3.select("#area-chart").append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")")

// Scales
const x_area_scale = d3.scaleBand().range([0, widtha]).padding(0.2)
const y_area_scale = d3.scaleLinear().range([0, heighta])

// Axis
const yAxis_area = d3.axisLeft(y_area_scale).ticks(5)
const xAxis_area = d3.axisBottom(x_area_scale)
const y_axis_area = ga.append("g").attr("class", "y axis")
const x_axis_area = ga.append("g").attr("class", "x axis").attr("transform", "translate(0, " + heighta + ")")

// Y-Axis label
const y_label_area = y_axis_area.append("text")
	  .attr("class", "axis-title")
    .attr("y", 6)
    .attr("transform", "rotate(-90)")
    .attr("dy", "0.71em")
    .attr("text-anchor", "end")

// Time Format
const parseDate_area = d3.timeParse("%d-%b-%y")

// Obtain Data
// ***********

// Init Variabes
const y_data = "COUNT", x_data = "MES_INGRESO"
const y_max = d3.max(dataa, d => d[y_data])
const x_ranges = dataa.map(d => d[x_data])
y_area_scale.domain([y_max, 0])
x_area_scale.domain(x_ranges)

// Area Chart
const area = d3.area()
  .x(d => x_area_scale(d[x_data]))
	.y0(y_area_scale(0))
  .y1(d => y_area_scale(d[y_data]))

ga.append("path")
  .attr("fill", "#C6DCEA")
  .attr("stroke", "#95B0C1")
  .attr("stroke-width", 1.5)
	.attr("d", area(dataa))

configAxisAndLabels(x_area_scale, y_area_scale, "#000")

// Config Axis
// ***********
function configAxisAndLabels(x, y, color) {

	// Y Axis
	y_axis_area.call(yAxis_area).selectAll("text").style("fill", color)

	// X Axis
	x_axis_area.call(xAxis_area).selectAll("text").style("fill", color)
		.attr("y", "10").attr("x", "-5")
		.attr("text-anchor", "end")
		.attr("transform", "rotate(-45)")

	// Axis Color
	ga.selectAll(".y.axis line").style("stroke", color)
	ga.selectAll(".y.axis path").style("stroke", color)
	ga.selectAll(".x.axis line").style("stroke", color)
	ga.selectAll(".x.axis path").style("stroke", color)

  // Label
  y_label_area.text("# Cases").style("fill", color)

}

// NOTES:
// https://github.com/d3/d3-scale-chromatic
