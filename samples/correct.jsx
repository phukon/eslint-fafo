import React from 'react';
import { useEffect } from 'rect';

class MyComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      message: 'Hello, World!',
    }
  }

  handleClick = () => {
    this.setState({ message: 'Button clicked!' });
  };

  render() {
    return (
      <div>
        <h1>{this.state.message}</h1>
        <button onClick={this.handleClick}>Click me</button>
      </div>
    );
  }
}

export default MyComponent;
