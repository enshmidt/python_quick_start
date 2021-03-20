import pkg_resources

def main():
  path = "example.txt"
  filepath = pkg_resources.resource_filename(__name__, path)
  print("I am main!!!")
  for l in open(filepath, 'r'):
    print(l)

if __name__ == '__main__':
  main()