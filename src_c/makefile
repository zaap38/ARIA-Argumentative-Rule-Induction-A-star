# Specify the compiler
CXX = g++

# Specify compiler flags
CXXFLAGS = -std=c++17 -Wno-Wsign-compare

# Specify the target executable
TARGET = gaari.exe

# Specify the source files
SRCS = main.cpp astar.cpp node.cpp af.cpp argument.cpp snippets.cpp dataset.cpp

# Specify the object files
OBJS = $(SRCS:.cpp=.o)

# Default target
all: $(TARGET)

# Compile source files into object files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Link object files into the executable
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $(TARGET)

# Clean up object files and executable
clean:
	rm -f $(OBJS) $(TARGET)