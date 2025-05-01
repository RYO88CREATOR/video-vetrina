fetch('videos.json')
  .then(response => response.json())
  .then(data => {
    const container = document.getElementById('video-list');
    data.forEach(video => {
      const div = document.createElement('div');
      div.innerHTML = `<a href="player.html?video=${encodeURIComponent(video.videoUrl)}">${video.title}</a>`;
      container.appendChild(div);
    });
  });