const get = async (url: string) => {
  console.log(url + window.location.search);
  const res = await fetch(url + window.location.search);
  const data = await res.json();
  if (!data['data']) {
    return data;
  }
  return data.data;
};

export default get