import React, { useEffect } from 'react';
import Chart from 'chart.js/auto'
import { Line } from 'react-chartjs-2';
import axios from 'axios';


const Graph = () => {
  const [chartData, setChartData] = React.useState(null);

  const lastSevenDays = () => {
    const dates = [];
    const today = new Date();
    for (let i = 6; i >=0; i--) {
      const date = new Date(today);
      date.setDate(today.getDate() - i);
      dates.push(date.toISOString().slice(0, 10));
    }
    return dates;
  }


  useEffect(() => {
    axios.get('http://localhost:5000/data')
      .then(res => {
        const chartData = {
          labels: lastSevenDays(),
          datasets: [
            {
              label: "Nombre des requêtes bloquées les 7 derniers jours",
              data: res.data,
              borderColor: '#ff8500',
              backgroundColor: '#606060',
            }
          ],
        };
        setChartData(chartData);
      })
      .catch(err => {
        console.log(err);
      });
  }, []);


  if (!chartData) {
    return <div className='text-grey-color'>Loading...</div>;
  }

  return (
    <div className="rounded-md">
      <Line
        data={chartData}
        options={{
          plugins: {
            title: {
              display: true,
              text: "Nombre des requêtes bloquées les 7 derniers jours"
            },
            legend: {
              display: false
            }
          }
        }}
        className="mt-4"
      />
    </div>
  );
}

export default Graph;
