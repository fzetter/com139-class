// Config
const datab = bar_json
const marginb = {top: 30, bottom: 75, right: 40, left: 75}
const widthb = $("#bar-chart").width() - margin.left - margin.right
const heightb = $("#bar-chart").height() - margin.top - margin.bottom
const gb = d3.select("#bar-chart").append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")")

// Scales
const x_bar_scale = d3.scaleBand().range([0, widthb]).padding(0.2)
const y_bar_scale = d3.scaleLinear().range([0, heightb])

// Axis
const yAxis_bar = d3.axisLeft(y_bar_scale).ticks(6)
const xAxis_bar = d3.axisBottom(x_bar_scale)
const y_axis_bar = gb.append("g").attr("class", "y axis")
const x_axis_bar = gb.append("g").attr("class", "x axis").attr("transform", "translate(0, " + heightb + ")")

// Y-Axis label
const y_label_bar = y_axis_bar.append("text")
	  .attr("class", "axis-title")
    .attr("y", 6)
    .attr("transform", "rotate(-90)")
    .attr("dy", "0.71em")
    .attr("text-anchor", "end")

// Obtain Data
// ***********

// Init Variabes
const y_data_bar = "COUNT", x_data_bar = "ENTIDAD_RES"
const y_max_bar = d3.max(datab, d => d[y_data_bar])
const x_ranges_bar = datab.map(d => d[x_data_bar])
y_bar_scale.domain([y_max_bar, 0])
x_bar_scale.domain(x_ranges_bar)

// Bar Chart
rect = gb.selectAll("rect").data(datab)
rect.enter()
    .append("rect")
    .attr("x", (d, i) => x_bar_scale(d[x_data_bar]))
    .attr("y", d => y_bar_scale(d[y_data_bar]))
    .attr("width", d => x_bar_scale.bandwidth())
    .attr("height", d => height - y_bar_scale(d[y_data_bar]))
    .attr("fill", (d, i) => d3.interpolateBrBG(i*0.040) )

configAxisAndLabelsB(x_bar_scale, y_bar_scale, "#000")

// Config Axis
// ***********
function configAxisAndLabelsB(x, y, color) {

	// Y Axis
	y_axis_bar.call(yAxis_bar).selectAll("text").style("fill", color)

	// X Axis
	x_axis_bar.call(xAxis_bar).selectAll("text").style("fill", color)
		.attr("y", "10").attr("x", "-5")
		.attr("text-anchor", "end")
		.attr("transform", "rotate(-45)")

	// Axis Color
	gb.selectAll(".y.axis line").style("stroke", color)
	gb.selectAll(".y.axis path").style("stroke", color)
	gb.selectAll(".x.axis line").style("stroke", color)
	gb.selectAll(".x.axis path").style("stroke", color)

  // Label
  y_label_bar.text("# Cases").style("fill", color)

}

// NOTES:
// https://github.com/d3/d3-scale-chromatic
