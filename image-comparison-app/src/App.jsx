import React, { useEffect, useState } from 'react';

function App() {
  const [pair, setPair] = useState(null);

  useEffect(() => {
    // Fetch the first pair when the component mounts
    fetchNextPair();
  }, []);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!pair) return;
      if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        const key = e.key === 'ArrowLeft' ? 'left' : 'right';
        // Send the response to the backend
        fetch('/record_response', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ pair_id: pair.a_image, key }),
        })
          .then((response) => response.json())
          .then((data) => {
            console.log('Response recorded:', data);
            // Fetch the next pair
            fetchNextPair();
          })
          .catch((error) => console.error(error));
      }
      if (e.key === 'ArrowUp') {
        fetchLastPair();
      }
    };

    // Add event listener for key presses
    window.addEventListener('keydown', handleKeyDown);

    // Cleanup to remove the event listener
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [pair]);

  const fetchLastPair = () => {
    fetch('/last_pair')
      .then((response) => {
        if (response.ok) return response.json();
        else throw new Error('No more image pairs.');
      })
      .then((data) => {
        setPair(data);
      })
      .catch((error) => {
        console.error(error);
        setPair(null);
      });
  }
  const fetchNextPair = () => {
    fetch('/next_pair')
      .then((response) => {
        if (response.ok) return response.json();
        else throw new Error('No more image pairs.');
      })
      .then((data) => {
        setPair(data);
      })
      .catch((error) => {
        console.error(error);
        setPair(null);
      });
  };


  if (!pair) {
    return <div>No more image pairs.</div>;
  }

  return (
    <div>
      <div style={{ display: 'flex' }}>
        <img src={pair.a_image} alt="A" style={{ width: '50%' }} />
        <img src={pair.b_image} alt="B" style={{ width: '50%' }} />
      </div>
      <p>Press left or right arrow key to choose.</p>
    </div>
  );
}

export default App;
