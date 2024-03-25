const get = async (url: string) => {
  const res = await fetch(url + window.location.search);
  const data = await res.json();
  if (data['login_url']) {
    window.location.href = data["login_url"];
    return;
  }
  return data;
};

export default get