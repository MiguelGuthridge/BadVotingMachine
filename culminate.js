async function culminate() {
  let res = await fetch(
    'http://127.0.0.1:5001/culminate',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    }
  );
  console.log(await res.text());
}

culminate();
