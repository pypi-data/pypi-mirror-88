# This file is generated automatically by scripts
import kimpy

attributes = [
  kimpy.charge_unit.unused,
  kimpy.charge_unit.C,
  kimpy.charge_unit.e,
  kimpy.charge_unit.statC,
]


str_names = [
  "unused",
  "C",
  "e",
  "statC",
]


def test_main():
    """Main test function."""

    N = kimpy.charge_unit.get_number_of_charge_units()
    assert N == 4

    all_instances = []
    for i in range(N):
        inst,error = kimpy.charge_unit.get_charge_unit(i)
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
    inst,error = kimpy.charge_unit.get_charge_unit(N)
    assert error == True

if __name__ == '__main__':
    test_main()
