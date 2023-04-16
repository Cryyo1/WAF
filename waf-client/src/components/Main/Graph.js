import React,{useEffect} from 'react';
import Chart from 'chart.js/auto'
import { Line } from 'react-chartjs-2';
import axios from 'axios';


const Graph = () => {
    const [chartData,setChartData] = React.useState(null);
    
    useEffect(() => {
      axios.get('http://localhost:5000/data')
        .then(res => {
          const chartData = {
            labels: res.data.map((item) => item['day']),
            datasets: [
              {
                label: "Nombre des requêtes bloquées les 7 derniers jours",
                data: res.data.map((item) => item['total blocks']),
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
        />
      </div>
    );
  }
  
  export default Graph;
  