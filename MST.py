import re
from typing import Tuple, Dict, List, Union
from str_filters import filter_value


class MSTBlock:
    """MST_DATA Block class."""
    
    def __init__(self, block_name: str, block_content: str, name: str = None):
        self.__name = name
        self.block_name = block_name
        self.block_content = block_content
        self.__block_dict, self.__blocks_count = get_blocks(block_content)
    
    def get_block(self, name: str) -> str:
        """
        Get block content from MST_DATA string.

        :param name: Block name
        :return: block_content
        """
        return self.__block_dict[name]
    
    @staticmethod
    def __get_kv_pairs(block_content: str):
        """Create key-value pairs from block content."""
        kv_pattern = r"^\s*?(?P<key>\w+)\s+(?P<value>.+)$"
        reg_pattern = re.compile(kv_pattern, re.M)
        
        match_iter = reg_pattern.finditer(block_content)
        kv_pairs = {}
        for match in match_iter:
            key = match.groupdict()["key"]
            value = match.groupdict()["value"]
            
            kv_pairs[key] = value
        
        return kv_pairs
    
    def check_content_match(self, other: "MSTBlock", reports: Union[None, List[str]] = None) -> Tuple[bool, List[str]]:
        """
        """
        kv_pair_1 = self.__get_kv_pairs(self.block_content)
        kv_pair_2 = self.__get_kv_pairs(other.block_content)
        other_name = other.name if other.name else "2nd block"
        self_name = self.name if self.name else "1st block"
        
        if reports is None:
            reports = []
        
        has_error = False
        reported_mismatch = set()
        reported_missing = set()
        
        for key, value in kv_pair_1.items():
            if key not in kv_pair_2:
                reports.append(f"\tKey {key} not found in {other_name}: {other.block_name}")
                has_error = True
                reported_missing.add(key)
            
            elif filter_value(value) != filter_value(kv_pair_2[key]):
                reports.append(f"\tValue mismatch for key {key} in block {other_name}: {other.block_name}\n"
                               f"\t\tValue 1: {value}\n"
                               f"\t\tValue 2: {kv_pair_2[key]}")
                has_error = True
                reported_mismatch.add(key)
        
        for key, value in kv_pair_2.items():
            if key in reported_mismatch or key in reported_missing:
                continue
            
            if key not in kv_pair_1:
                reports.append(f"\tKey {key} not found in {self_name}: {self.block_name}")
                has_error = True
            
            elif filter_value(value) != filter_value(kv_pair_1[key]):
                reports.append(f"\tValue mismatch for key {key} in block {self_name}: {self.block_name}\n"
                               f"\t\tValue 1: {value}\n"
                               f"\t\tValue 2: {kv_pair_1[key]}")
                has_error = True
        
        return not has_error, reports
    
    @property
    def blocks_count(self):
        return self.__blocks_count
    
    @property
    def name(self):
        return self.__name
    
    def __eq__(self, other: "MSTBlock"):
        is_match, _ = self.check_content_match(other)
        return self.block_name == other.block_name and is_match
    
    def __ne__(self, other: "MSTBlock"):
        return not self.__eq__(other)
    
    def __repr__(self):
        return f"MSTBlock(block_name={self.block_name}, block_content={self.block_content})"
    
    def __str__(self):
        return f"MSTBlock(block_name={self.block_name}, block_content={self.block_content})"


class MST:
    def __init__(self, mst_string: str, name: str = None):
        self.__blocks_dict = {}
        self.__blocks_count = 0
        self.name = name
        self.__parse_mst_string(mst_string)
    
    def __parse_mst_string(self, mst_string: str):
        comments_pattern = r"\s+?//.+$"
        # remove comments
        mst_string = re.sub(comments_pattern, "", mst_string, flags=re.M)
        
        blocks_pattern = r"BEGIN (?P<block_name>[\w ]+)\n.+?END"
        reg_pattern = re.compile(blocks_pattern, re.M | re.S)
        
        match_iter = reg_pattern.finditer(mst_string)
        for match in match_iter:
            block_name = match.groupdict()["block_name"]
            block_content = match.group(0)
            
            self.add_block(block_name, block_content)
    
    def add_block(self, block_name: str, block_content: str):
        self.__blocks_dict[block_name] = MSTBlock(block_name, block_content, name=self.name)
        self.__blocks_count += 1
    
    def get_block(self, block_name: str) -> MSTBlock:
        return self.__blocks_dict[block_name]
    
    def compare(self, other: "MST"):
        complete_reports_str = ""
        has_error = False
        
        if self.__blocks_count != other.__blocks_count:
            complete_reports_str += f"\n\nBlock count mismatch: {self.__blocks_count} != {other.__blocks_count}"
            has_error = True
        
        missing_blocks = self.__blocks_dict.keys() - other.__blocks_dict.keys()
        if missing_blocks:
            missing_blocks_str = "\n".join(missing_blocks)
            complete_reports_str += f"Missing blocks:\n" \
                                    f"{missing_blocks_str}"
            has_error = True
        
        extra_blocks = other.__blocks_dict.keys() - self.__blocks_dict.keys()
        if extra_blocks:
            extra_blocks_str = "\n".join(extra_blocks)
            complete_reports_str += f"Extra blocks:\n" \
                                    f"{extra_blocks_str}"
            has_error = True
        
        for block_name, block in self.__blocks_dict.items():
            if block_name in other.__blocks_dict:
                other_block = other.__blocks_dict[block_name]
                is_match, block_reports = block.check_content_match(other_block)
                if not is_match:
                    complete_reports_str += f"\n\nBlock {block_name} content mismatch:"
                    reports_str = "\n\n\t".join(block_reports)
                    complete_reports_str += f"\n\t{reports_str}"
                    has_error = True
        
        return not has_error, complete_reports_str
    
    def __eq__(self, other: "MST"):
        has_match, _ = self.compare(other)
        return has_match


def get_blocks(mst_string: str) -> Tuple[Dict[str, str], int]:
    """
    Get blocks from MST_DATA string.

    :param mst_string: MST_DATA string
    :return: blocks_dict, blocks_count
    """
    blocks_pattern = r"BEGIN (?P<block_name>[\w ]+)\n.+?END"
    reg_pattern = re.compile(blocks_pattern, re.M | re.S)
    match_iter = reg_pattern.finditer(mst_string)
    blocks_count = 0
    blocks_dict = {}
    
    for match in match_iter:
        blocks_count += 1
        block_content = match.group()
        block_name = match.groupdict()["block_name"]
        
        blocks_dict[block_name] = block_content
    
    return blocks_dict, blocks_count
