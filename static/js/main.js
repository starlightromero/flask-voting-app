window.addEventListener('DOMContentLoaded', () => {
  // We are wrapping everything in an event listener 'DOMContentLoaded'
  // This ensures that the window is loaded before we try to connect
  // and set sockets

  // TODO: create a calculatePercentage function that takes in results and sets
  // the width of the progress bar along with the innerHTML
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

  // TODO: create an updateCandidates function that takes in cadidates and sets
  // the candidates image and name
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

  // TODO: make an axios get request to '/results' to get the voting results
  //  then pass the data to calculatePercentage to update the results on the page
  axios.get('/results').then(response => {
    calculatePercentage(response.data)
  }).catch(err => {
    console.log(err)
  })

  // TODO: create a getCandidates function. In the function make an axios get request
  // to '/candidates' and pass the data to updateCandidates
  const getCandidates = () => {
    axios.get('/candidates').then(response => {
      updateCandidates(response.data)
    }).catch(err => {
      console.log(err)
    })
  }

  // TODO: call the getCandidates function
  getCandidates()

  // TODO: connect to sockets
  let socket = io.connect('http://127.0.0.1:5000')

  // TODO: add an event listener on vote1 that will emit a vote on click
  document.getElementById('vote1').addEventListener('click', () => {
    socket.emit('vote', 1)
  })

  // TODO: add an event listener on vote2 that will emit a vote on click
  document.getElementById('vote2').addEventListener('click', () => {
    socket.emit('vote', 2)
  })

  // TODO: create a socket on 'vote_results' function that takes in results and
  // passes the data to calculatePercentage
  socket.on('vote_results', results => {
    calculatePercentage(results)
  })

  // TODO: create an event listener on upload that will getCandidates
  document.getElementById('upload').addEventListener('click', () => {
    getCandidates()
  })
})
