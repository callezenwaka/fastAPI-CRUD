import fetch from 'node-fetch';
export const url = 'https://jsonplaceholder.typicode.com/posts/';
// const url = 'https://jsonplaceholder.typicode.com/todos/';

export const getAnimals = async () => {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Error! status: ${response.status}`);
  }

  const data = await response.json();

  return data;
}

export const getAnimal = async (id) => {
  const response = await fetch(url + id);

  if (!response.ok) {
    throw new Error(`Error! status: ${response.status}`);
  }

  const data = await response.json();

  return data;
}

export const dependencyInjection = async (fetch, id) => {

  const response = await fetch(url + id);

  // if (!response.ok) {
  //   throw new Error(`Error! status: ${response.status}`);
  // }

  const data = await response.json();

  return data;

}
// console.info(await getAnimals());
// console.info(await getAnimal(1));
// console.info(await dependencyInjection(,1));
