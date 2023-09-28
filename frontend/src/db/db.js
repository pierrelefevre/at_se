import { MongoClient } from 'mongodb';

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

export const getStories = () => {
  const stories = getCollection("stories").find({}).toArray();
  return stories;
};

export const getGroups = () => {
  const groups = getCollection("groups").find({}).toArray();
  return groups;
};
