# This file is generated automatically by scripts
import kimpy

attributes = [
  kimpy.numbering.zeroBased,
  kimpy.numbering.oneBased,
]


str_names = [
  "zeroBased",
  "oneBased",
]


def test_main():
    """Main test function."""

    N = kimpy.numbering.get_number_of_numberings()
    assert N == 2

    all_instances = []
    for i in range(N):
        inst,error = kimpy.numbering.get_numbering(i)
        all_instances.append(inst)

        assert error == False
        assert inst == attributes[i]
        assert str(inst) == str_names[i]

    # test operator overloading
    for i in range(N):
        assert all_instances[i] == all_instances[i]
        for j in range(i+1, N):
            assert all_instances[i] != all_instances[j]

    # test known
    for inst in all_instances:
        assert inst.known() == True

    # test out of bound
    inst,error = kimpy.numbering.get_numbering(N)
    assert error == True

if __name__ == '__main__':
    test_main()
