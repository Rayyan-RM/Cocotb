-- Date : 19/05/2026
-- Author : Reiyan RM
-- Company : Thakshana Technologies Pvt Ltd.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity counter is
    generic (
        WIDTH : integer := 8
    );
    port (
        clk     : in  std_logic;
        arstn     : in  std_logic;  --asynchronize reset active on LOW
        en      : in  std_logic; -- componennt will be operate when enable = 1 
        count   : out std_logic_vector(WIDTH-1 downto 0)  
    );
end entity counter;

architecture rtl of counter is

     signal counter_reg : std_logic_vector(WIDTH-1 downto 0) := (others => '0');
    signal next_counter : std_logic_vector(WIDTH-1 downto 0);

begin

next_counter <= std_logic_vector(unsigned(counter_reg)+1) when en = '1' else 
                counter_reg ;

 process(clk)
 begin
    if rising_edge (clk) then 
        if arstn = '0' then 
            counter_reg <= (others => '0');
        else
            counter_reg <= next_counter;
        end if ;  
     end if;      
 end process;

count <=  counter_reg; 

end architecture rtl;
