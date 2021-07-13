// Config
// ******
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
const x_scale = d3.scaleLog().domain([142, 150000]).range([0, width]).base(10)
const y_scale = d3.scaleLinear().domain([90, 0]).range([0, height])
const area_scale = d3.scaleLinear().domain([2000, 1400000000]).range([25*Math.PI, 1500*Math.PI])
const continents = ["africa", "americas", "asia", "europe"]
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
	.attr("x", (width / 2) - 70)
	.attr("y", height + 60)
	.attr("font-size", "15px")

const year_label = g.append("text")
	.attr("class", "x axis-label")
	.attr("x", width - 130)
	.attr("y", height - 20)
	.attr("font-size", "55px")

const legend = g.append("g")
	.attr("transform", "translate(" + (width - 10) + "," + (height - 125) + ")")

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
		.attr("text-anchor", "end")
		.style("text-transform", "capitalize")
		.text(continent)
})

// Obtain Data
// ***********
data = parse(data)
let len = data.length-2, curr = 190

d3.interval(() => {
	if (curr > len) curr = 0
	else curr += 1
	update(data[curr].countries, data[curr].year)
}, 100)
update(data[curr].countries, data[curr].year)

// Update Data
// ***********
function update(data, year) {

	// Join
	circle = g.selectAll("circle").data(data, d => d.country)
	// Exit
	circle.exit().remove()
	// Enter & Update
	circle.enter().append("circle")
		.attr("cx", d => x_scale(d.income))
		.attr("cy", d => y_scale(d.life_exp))
		.attr("r", d => Math.sqrt(area_scale(0) / Math.PI))
		.attr("fill", d => color_scale(d.continent))
		.merge(circle)
		.transition(t)
			.attr("cx", d => x_scale(d.income))
			.attr("cy", d => y_scale(d.life_exp))
			.attr("r", d => Math.sqrt(area_scale(d.population) / Math.PI))

	configAxisAndLabels(x_scale, y_scale, "#000", "Life Expectancy (Years)", "GDP Per Capita ($)", year)

}

// Config Axis & Labels
// *********************
function configAxisAndLabels(x, y, color, yLabel, xLabel, yearLabel) {

	// Y Axis
	const yAxis = d3.axisLeft(y)
	y_axis.transition(t).call(yAxis).selectAll("text").style("fill", color)

	// X Axis
	const xAxis = d3.axisBottom(x).tickValues([400, 4000, 40000]).tickFormat(d => "$" + d)
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
	year_label.text(yearLabel).style("fill", color).style("fill-opacity", "0.5")

	// Legend
	g.selectAll(".legend").style("fill", color)

}

// Parse Integers
// **************
function parse(data) {
	data = data.map(item => {
		return {
			countries: item.countries
				 .filter(country => country.income && country.life_exp)
				 .map(country => {
						country.income = +country.income
						country.life_exp = +country.life_exp
						return country
				 }),
		  year: item.year
		}
	})
  return data
}

// NOTES:
// https://github.com/d3/d3-scale-chromatic
