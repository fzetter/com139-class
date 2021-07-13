// Config
// ******
const data = scatter_json
const margin = {top: 30, bottom: 75, right: 40, left: 75}
const width = $("#scatter-plot").width() - margin.left - margin.right
const height = $("#scatter-plot").height() - margin.top - margin.bottom
const g = d3.select("#scatter-plot").append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")")

/* Scales:
	x: Income
	y: Age Expectancy
	area: Population
	color: Country
*/
const x_scale = d3.scaleLinear().range([0, width])
const y_scale = d3.scaleLinear().range([0, height])
const area_scale = d3.scaleLinear().domain([10, 10000]).range([25*Math.PI, 1500*Math.PI])
const continents = ['NEUMONIA','DIABETES','EPOC','ASMA','INMUSUPR','HIPERTENSION','CARDIOVASCULAR','OBESIDAD','RENAL_CRONICA','TABAQUISMO']
const color_scale = d3.scaleOrdinal().domain(continents).range(d3.schemeSet3)

const y_axis = g.append("g").attr("class", "y axis")
const x_axis = g.append("g").attr("class", "x axis").attr("transform", "translate(0, " + height + ")")
const t = 750

const y_label = g.append("text")
	.attr("class", "y axis-label")
	.attr("x", - (height / 2))
	.attr("y", -45)
	.attr("font-size", "15px")
	.attr("text-anchor", "middle")
	.attr("transform", "rotate(-90)")

const x_label =	g.append("text")
	.attr("class", "x axis-label")
	.attr("x", (width / 2) - 35)
	.attr("y", height + 60)
	.attr("font-size", "15px")

const month_label = g.append("text")
	.attr("class", "x axis-label")
	.attr("x", width - 95)
	.attr("y", height - 20)
	.attr("font-size", "50px")

const legend = g.append("g")
	.attr("transform", "translate(" + width + "," + (height / 2 - 50) + ")")

continents.forEach((continent, i) => {
	const legendRow = legend.append("g").attr("transform", "translate(-15, " + ((i * 20)-30) + ")")
	legendRow.append("rect")
		.attr("width", 10)
		.attr("height", 10)
		.attr("fill", color_scale(continent))
	legendRow.append("text")
	  .attr("class", "legend")
		.attr("x", -10)
		.attr("y", 10)
		.attr("font-size", "10px")
		.attr("text-anchor", "end")
		.style("text-transform", "capitalize")
		.text(continent)
})

// Obtain Data
// ***********
let len = data.length-2, curr = 3

d3.interval(() => {
	if (curr > len) curr = 0
	else curr += 1
	update(data[curr].conditions, data[curr].month)
}, 700)
update(data[curr].conditions, data[curr].month)

// Update Data
// ***********
function update(data, month) {

	x_scale.domain([0, 900])
	y_scale.domain([900, 0])

	// Join
	circle = g.selectAll("circle").data(data, d => d.name)
	// Exit
	circle.exit().remove()
	// Enter & Update
	circle.enter().append("circle")
		.attr("cx", d => x_scale(d.deaths))
		.attr("cy", d => y_scale(d.count))
		.attr("r", d => Math.sqrt(area_scale(0) / Math.PI))
		.attr("fill", d => color_scale(d.name))
		.merge(circle)
		.transition(t)
			.attr("cx", d => x_scale(d.deaths))
			.attr("cy", d => y_scale(d.count))
			.attr("r", d => Math.sqrt(area_scale(d.count) / Math.PI))

	configAxisAndLabels(x_scale, y_scale, "#000", "Cases", "Deaths", month)

}

// Config Axis & Labels
// *********************
function configAxisAndLabels(x, y, color, yLabel, xLabel, monthLabel) {

	// Y Axis
	const yAxis = d3.axisLeft(y)
	y_axis.transition(t).call(yAxis).selectAll("text").style("fill", color)

	// X Axis
	const xAxis = d3.axisBottom(x)
	x_axis.call(xAxis).selectAll("text").style("fill", color)
		.attr("y", "10").attr("x", "-5")
		.attr("text-anchor", "end")
		.attr("transform", "rotate(-45)")

	// Axis Color
	g.selectAll(".y.axis line").style("stroke", color)
	g.selectAll(".y.axis path").style("stroke", color)
	g.selectAll(".x.axis line").style("stroke", color)
	g.selectAll(".x.axis path").style("stroke", color)

	// Labels
	y_label.text(yLabel).style("fill", color)
	x_label.text(xLabel).style("fill", color)
	month_label.text(monthLabel).style("fill", color).style("fill-opacity", "0.5")

	// Legend
	g.selectAll(".legend").style("fill", color)

}

// NOTES:
// https://github.com/d3/d3-scale-chromatic
