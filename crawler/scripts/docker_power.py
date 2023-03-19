with open('/sys/fs/cgroup/cpu.max') as cgroup_file:
    line = cgroup_file.readline()
    nums = line.split(' ')
    if nums[0] == 'max':
        print(1)
    else:
        print(int(nums[0]) / int(nums[1]))
