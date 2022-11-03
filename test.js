import { expect } from "chai";
import { getAnimal, dependencyInjection } from "./index.js";

describe("Dependency Injection", async function () {
  const postId = 1;
  const userId = 1;
  const post = {
    userId: 1,
    id: 1,
    title: 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
    body: 'quia et suscipit\n' +
      'suscipit recusandae consequuntur expedita et cum\n' +
      'reprehenderit molestiae ut ut quas totam\n' +
      'nostrum rerum est autem sunt rem eveniet architecto'
  };

  // before(async () => {

  //   const Utils = await ethers.getContractFactory("Utils");
  //   utils = await Utils.deploy();
  //   await utils.deployed();
  //   console.log("Utils deployed to:", utils.address);
  // });

  it("Calls fetch with the correct url!", async function () {
    const fakeFetch = url => {
      expect(url).to.equal('https://jsonplaceholder.typicode.com/posts/'+1);

      return new Promise(function(resolve) {});
    }

    dependencyInjection(fakeFetch, postId);
  });

  it("Parses the response of fetch correctly!", async function () {
    const fakeFetch = url => {
      return Promise.resolve({
        json: () => Promise.resolve({ post })
      });
    }

    const response = await dependencyInjection(fakeFetch, postId);
    expect(response.post.userId).to.equal(userId);
    expect(response.post.id).to.equal(postId);
    expect(response.post.title).to.equal('sunt aut facere repellat provident occaecati excepturi optio reprehenderit');
    // expect(result2).to.be.a('boolean');
  });
});