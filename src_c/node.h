

class Node<T> {

    public:
        int getDistance() const;
        int getColor() const;
        T * getValue() const;

        void setColor(int color);
        void setDistance(int distance);

    private:
        T *_value;
        int _color;  // 0: white; 1: grey; 2: black
        int _distance;

};