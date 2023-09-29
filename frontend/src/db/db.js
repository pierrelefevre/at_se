import { MongoClient } from "mongodb";

export const getClient = () => {
  const uri = import.meta.env.MONGO_URI;
  if (!uri) {
    throw new Error("Please define the MONGO_URI environment variable");
  }
  const client = new MongoClient(uri);
  return client;
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
  const stories = await getCollection("stories").find({}).toArray();
  return stories;
};

export const getGroups = async () => {
  const groups = await getCollection("groups").find({}).toArray();
  return groups;
};