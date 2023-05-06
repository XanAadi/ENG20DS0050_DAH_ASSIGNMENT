import threading

class MapReduce:
    def __init__(self, input_data):
        self.input_data = input_data
        self.intermediate = {}
        self.lock = threading.Lock()
    
    def map(self, record):
        # Split the record into words
        words = record.split()
        for word in words:
            # Emit a key-value pair for each word
            with self.lock:
                if word in self.intermediate:
                    self.intermediate[word] += 1
                else:
                    self.intermediate[word] = 1
    
    def reduce(self, key):
        # Sum the values for each key
        return sum(self.intermediate[key])
    
    def execute(self):
        # Split the input data into records
        records = self.input_data.split("\n")
        
        # Create mapper threads
        mapper_threads = []
        for record in records:
            mapper_thread = threading.Thread(target=self.map, args=(record,))
            mapper_threads.append(mapper_thread)
            mapper_thread.start()
        
        # Wait for all mapper threads to finish
        for mapper_thread in mapper_threads:
            mapper_thread.join()
        
        # Create reducer threads
        reducer_threads = []
        for key in self.intermediate.keys():
            reducer_thread = threading.Thread(target=self.reduce, args=(key,))
            reducer_threads.append(reducer_thread)
            reducer_thread.start()
        
        # Wait for all reducer threads to finish
        for reducer_thread in reducer_threads:
            reducer_thread.join()
        
        # Return the final results
        return self.intermediate


input_data = "Hello world\nHello Python\nPython is awesome\n"
mr = MapReduce(input_data)
result = mr.execute()
print(result)
