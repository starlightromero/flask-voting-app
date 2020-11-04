window.addEventListener('DOMContentLoaded', () => {
  const calculatePercentage = results => {
    const totalVotes = results.results1 + results.results2

    const vote1Percentage = Math.round(results.results1 / totalVotes * 100)
    const vote2Percentage = 100 - vote1Percentage

    if (vote1Percentage || vote2Percentage) {
      document.getElementById('results1').style.width = `${vote1Percentage}%`
      document.getElementById('results2').style.width = `${vote2Percentage}%`

      document.getElementById('results1').innerHTML = `${vote1Percentage}%`
      document.getElementById('results2').innerHTML = `${vote2Percentage}%`
    }
  }

  const updateCandidates = candidates => {
    if (candidates.candidate1_name && candidates.candidate1_image) {
      document.getElementById('candidate1_image').src = `static/images/${candidates.candidate1_image}`
      document.getElementById('vote1').innerHTML = candidates.candidate1_name
    }

    if (candidates.candidate2_name && candidates.candidate2_image) {
      document.getElementById('candidate2_image').src = `static/images/${candidates.candidate2_image}`
      document.getElementById('vote2').innerHTML = candidates.candidate2_name
    }
  }

  axios.get('/results').then(response => {
    calculatePercentage(response.data)
  }).catch(err => {
    console.log(err)
  })

  const getCandidates = () => {
    axios.get('/candidates').then(response => {
      updateCandidates(response.data)
    }).catch(err => {
      console.log(err)
    })
  }

  getCandidates()

  let socket = io.connect('http://127.0.0.1:5000')

  document.getElementById('vote1').addEventListener('click', () => {
    socket.emit('vote', 1)
  })

  document.getElementById('vote2').addEventListener('click', () => {
    socket.emit('vote', 2)
  })

  socket.on('vote_results', results => {
    calculatePercentage(results)
  })

  document.getElementById('upload').addEventListener('click', () => {
    getCandidates()
  })
})
