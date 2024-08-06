import { useRef, useEffect } from 'react';
import * as d3 from 'd3';

const CirclePack = ({ data }) => {
  const svgRef = useRef(null);

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const width = 1000;
    const height = 1000;

    const color = d3.scaleSequential([0, 5], d3.interpolateCool);

    const pack = d3.pack()
      .size([width, height])
      .padding(3);

    const root = d3.hierarchy(data)
      .sum(d => d.value)
      .sort((a, b) => b.value - a.value);

    const nodes = pack(root).descendants();

    svg
      .attr('viewBox', [0, 0, width, height])
      .attr('width', width)
      .attr('height', height)
      .style('font-weight', '700')

    const g = svg.append('g')
      .attr('transform', `translate(0, 0)`);

    const circle = g.selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('transform', d => `translate(${d.x},${d.y})`)
      .attr('r', d => d.r - (d.depth * 10))
      .attr('fill', d => color(d.depth))
      .attr('stroke', '#ccc')
      .attr('stroke-width', 1)
      .style('cursor', 'pointer')
      .on('click', (event, d) => zoom(event, d))
      .on('mouseover', function() {
        d3.select(this).style('cursor', 'pointer');
      })
      .on('mouseout', function() {
        d3.select(this).style('cursor', 'default');
      });

    const text = g.selectAll('text')
      .data(nodes)
      .join('text')
      .attr('transform', d => {
        const yOffset = d.children ? -d.r + 40 : 0;
        return `translate(${d.x},${d.y + yOffset})`;
      })
      .attr('dy', d => (d.children ? '-0.5em' : '0.3em'))
      .attr('text-anchor', 'middle')
      .attr('font-size', d => `${20 - d.depth * 1.5}`)
      .attr('color', '#ccc')
      .text(d => d.data.name);

    let view = [width, height, width];

    const zoomTo = v => {
      const k = width / v[2];
      view = v;
      g.attr("transform", `translate(${width / 2 - v[0] * k},${height / 2 - v[1] * k}) scale(${k})`);
    };

    const zoom = (event, d) => {
      const v = [d.x, d.y, d.r * (d === root ? 2 : 3)];
      svg.transition()
        .duration(750)
        .tween('zoom', () => {
          const i = d3.interpolateZoom(view, v);
          return t => zoomTo(i(t));
        });

      // Set reduced opacity for non-zoomed circles
      circle.transition().duration(750)
        .style('opacity', node => node === d || node.parent === d ? 1 : 0.2);

      text.transition().duration(750)
        .style('opacity', node => node === d || node.parent === d ? 1 : 0.2);

      event.stopPropagation();
    };

    svg.on('click', (e) => {
      zoom(e, root);
      // Reset opacity for all circles
      circle.transition().duration(750).style('opacity', 1);
      text.transition().duration(750).style('opacity', 1);
    });

  }, [data]);

  return (
    <svg ref={svgRef}></svg>
  );
};

export default CirclePack;