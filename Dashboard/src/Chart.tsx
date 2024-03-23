import { ResponsiveChartContainer } from '@mui/x-charts/ResponsiveChartContainer';
import { LinePlot, MarkPlot} from '@mui/x-charts/LineChart';
import { BarPlot } from '@mui/x-charts/BarChart';
import { ChartsXAxis } from '@mui/x-charts/ChartsXAxis';
import { ChartsYAxis } from '@mui/x-charts/ChartsYAxis';
import { ChartsGrid } from '@mui/x-charts/ChartsGrid';
import { ChartsTooltip } from '@mui/x-charts/ChartsTooltip';
import { ChartsLegend } from '@mui/x-charts/ChartsLegend';

function ChartJS(props) {

    const series = [
        { type: 'line', dataKey: 'humid', color: '#577399',yAxisKey: 'rightAxis', label: 'Humid' },
        { type: 'bar', dataKey: 'temp', color: '#bfdbf7', yAxisKey: 'leftAxis' , label: 'Temp'},
    ];

    return (
        <>
         <ResponsiveChartContainer
          series={series}
          xAxis={[
            {
              scaleType: 'band',
              dataKey: 'time',
              label: 'Timer',
              reverse: false,
            },
          ]}
          yAxis={[
            { id: 'leftAxis', reverse: false },
            { id: 'rightAxis', reverse: false },
          ]}
          dataset={props.dataset}
          height={400}
        >
          <ChartsGrid horizontal />
          <BarPlot />
          <LinePlot />
          <MarkPlot />
          <ChartsLegend/>
          <ChartsTooltip />
          <ChartsXAxis />
          <ChartsYAxis axisId="leftAxis" position='left' label="Temerature (°C)" />
          <ChartsYAxis
            axisId="rightAxis"
            position="right"
            label="Humidity (%)"
          />
        </ResponsiveChartContainer>
        </>
    )
}

export default ChartJS