import { MongoClient } from "mongodb";

let cachedClient = null;

export const getClient = () => {
  const uri = import.meta.env.MONGO_URI;
  if (!uri) {
    throw new Error("Please define the MONGO_URI environment variable");
  }

  // check if client is already cached
  if (!cachedClient) {
    cachedClient = new MongoClient(uri);
  }

  // check if client is still connected
  checkMongoAlive(cachedClient).then((res) => {
    if (!res) {
      cachedClient = new MongoClient(uri);
    }
  });

  return cachedClient;
};

export const checkMongoAlive = async (client) => {
  await client.connect();
  const res = await client.db("admin").command({ ping: 1 });
  return res.ok === 1;
};

export const getDb = () => {
  const client = getClient();
  return client.db("at");
};

export const getCollection = (collection) => {
  const db = getDb();
  return db.collection(collection);
};

export const getStories = async () => {
  const stories = await getCollection("stories")
    .find({})
    .sort({ published_at: -1 })
    .toArray();
  return stories;
};

export const getGroups = async () => {
  const groups = await getCollection("groups").find({}).toArray();
  return groups;
};

export const getLatestStory = async () => {
  return getCollection("stories")
    .find({})
    .sort({ published_at: -1 })
    .limit(1)
    .toArray();
};

export const getStoriesById = async (ids) => {
  const stories = await getCollection("stories")
    .find({ id: { $in: ids } })
    .toArray();
  return stories;
};

export const getStoriesByTopic = async (topic) => {
  // find all stories with the given topic, not case sensitive.
  const stories = await getCollection("stories")
    .find({ category: { $regex: topic, $options: "i" } })
    .sort({ published_at: -1 })
    .toArray();
  return stories;
};

export const getStoryById = async (id) => {
  const story = await getCollection("stories").findOne({ id: id });
  return story;
};
