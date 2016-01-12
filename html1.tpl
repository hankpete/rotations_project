<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>3D Rotations</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <body>
    <div>
      <h1>Input the functions and parameters:</h1>
      <form role="form" method="post" action="/input">
          <div>
              Function to be rotated:
              <input type="text" name="function_a" placeholder="Function to be Rotated">
          </div>
          <div>
              Function to provide axis of rotation:
              <input type="text" name="function_b" placeholder="Function to provide axis of rotation">
          </div>
          <div>
              Minimum x value on the graph:
              <input type="text" name="MIN" placeholder="Min x value">
          </div>
          <div>
              Maximum x value on the graph:
              <input type="text" name="MAX" placeholder="Max x value">
          </div>
          <div>
          <button type="submit">Submit</button>
          </div>
      </form>
    </div>
  </body>
</html>
